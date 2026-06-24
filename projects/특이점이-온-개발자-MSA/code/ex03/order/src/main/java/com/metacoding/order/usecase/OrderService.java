package com.metacoding.order.usecase;

import com.metacoding.order.adapter.producer.OrderEventProducer;
import com.metacoding.order.core.handler.ex.*;
import com.metacoding.order.domain.*;
import com.metacoding.order.adapter.message.*;
import com.metacoding.order.repository.*;
import com.metacoding.order.web.dto.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@RequiredArgsConstructor
@Service
@Transactional(readOnly = true)
public class OrderService implements CreateOrderUseCase, GetOrderUseCase {

    private final OrderRepository orderRepository;
    private final OrderEventProducer orderEventProducer;

    @Override
    @Transactional
    public OrderResponse createOrder(int userId, int productId, int quantity, Long price, String address) {
        // 1. 주문 생성
        Order createdOrder = orderRepository.save(Order.create(userId, productId, quantity, price));
        createdOrder.validateMinAmount();

        // 2. Kafka로 주문 생성 이벤트 발행
        orderEventProducer.publishOrderCreated(
                new OrderCreatedEvent(createdOrder.getId(), userId, productId, quantity, price, address)
        );

        return OrderResponse.from(createdOrder);
    }

    @Transactional
    public void completeOrder(int orderId) {
        Order findOrder = orderRepository.findById(orderId)
                .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
        findOrder.complete();
    }

    @Override
    public OrderResponse findById(int orderId) {
        Order findOrder = orderRepository.findById(orderId)
                .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
        return OrderResponse.from(findOrder);
    }

    @Transactional
    public OrderResponse cancelOrder(int orderId) {
        Order findOrder = orderRepository.findById(orderId)
                .orElseThrow(() -> new Exception404("주문을 찾을 수 없습니다."));
        findOrder.cancel();
        return OrderResponse.from(findOrder);
    }
}
