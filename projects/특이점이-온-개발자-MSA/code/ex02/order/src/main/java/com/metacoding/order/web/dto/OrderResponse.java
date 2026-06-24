package com.metacoding.order.web.dto;

import com.metacoding.order.domain.*;
import java.time.LocalDateTime;

public record OrderResponse(
    int id,
    int userId,
    int productId,
    int quantity,
    Long price,
    OrderStatus status,
    LocalDateTime createdAt,
    LocalDateTime updatedAt
) {
    public static OrderResponse from(Order order) {
        return new OrderResponse(
            order.getId(),
            order.getUserId(),
            order.getProductId(),
            order.getQuantity(),
            order.getPrice(),
            order.getStatus(),
            order.getCreatedAt(),
            order.getUpdatedAt()
        );
    }
}
