package com.metacoding.order.web;

import com.metacoding.order.usecase.*;
import com.metacoding.order.web.dto.OrderRequest;
import org.springframework.http.ResponseEntity;
import com.metacoding.order.core.util.Resp;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {
    private final CreateOrderUseCase createOrderUseCase;
    private final GetOrderUseCase getOrderUseCase;

    @PostMapping
    public ResponseEntity<?> createOrder(@RequestBody OrderRequest requestDTO, @RequestAttribute("userId") Integer userId) {
        return Resp.ok(createOrderUseCase.createOrder(userId, requestDTO.productId(), requestDTO.quantity(), requestDTO.price(), requestDTO.address()));
    }

    @GetMapping("/{orderId}")
    public ResponseEntity<?> getOrder(@PathVariable("orderId") int orderId) {
        return Resp.ok(getOrderUseCase.findById(orderId));
    }
}
