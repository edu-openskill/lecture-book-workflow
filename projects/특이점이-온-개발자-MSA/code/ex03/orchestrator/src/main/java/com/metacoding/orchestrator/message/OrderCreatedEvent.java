package com.metacoding.orchestrator.message;

public record OrderCreatedEvent(
        int orderId,
        int userId,
        int productId,
        int quantity,
        Long price,
        String address
) {}
